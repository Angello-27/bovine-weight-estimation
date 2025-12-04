/// DataSource: MLRemoteDataSource
///
/// DataSource para predicciones de Machine Learning con el servidor.
/// Single Responsibility: Comunicación HTTP para predicciones ML.
///
/// Data Layer - Clean Architecture
library;

import 'dart:io';

import 'package:dio/dio.dart';

import '../../core/config/api_config.dart';
import '../../core/errors/exceptions.dart';
import '../../core/network/http_error_handler.dart';
import '../models/ml_models.dart';

/// DataSource para predicciones ML remotas con backend
abstract class MLRemoteDataSource {
  /// Predice peso de bovino usando IA del servidor
  ///
  /// Endpoint: POST /api/v1/ml/predict
  Future<WeightPredictionResponseModel> predictWeight({
    required File imageFile,
    required String breed,
    String? animalId,
    String? deviceId,
  });

  /// Obtiene el estado de los modelos ML en el servidor
  ///
  /// Endpoint: GET /api/v1/ml/models/status
  Future<MLModelsStatusResponseModel> getModelsStatus();
}

/// Implementación con Dio
class MLRemoteDataSourceImpl implements MLRemoteDataSource {
  final Dio dio;

  MLRemoteDataSourceImpl({required this.dio});

  @override
  Future<WeightPredictionResponseModel> predictWeight({
    required File imageFile,
    required String breed,
    String? animalId,
    String? deviceId,
  }) async {
    try {
      // Crear FormData para multipart/form-data
      final formData = FormData.fromMap({
        'image': await MultipartFile.fromFile(
          imageFile.path,
          filename: 'cow_image.jpg',
        ),
        'breed': breed,
        if (animalId != null) 'animal_id': animalId,
        if (deviceId != null) 'device_id': deviceId,
      });

      final response = await dio.post(
        ApiConfig.mlPredictEndpoint,
        data: formData,
      );

      if (response.statusCode == 200) {
        return WeightPredictionResponseModel.fromJson(response.data);
      } else {
        throw ServerException(
          message: 'Error al predecir peso: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } on DioException catch (e) {
      throw HttpErrorHandler.handle(e);
    } catch (e) {
      if (e is AppException) {
        rethrow;
      }
      throw ServerException(message: 'Error inesperado al predecir peso: $e');
    }
  }

  @override
  Future<MLModelsStatusResponseModel> getModelsStatus() async {
    try {
      final response = await dio.get('${ApiConfig.apiPrefix}/ml/models/status');

      if (response.statusCode == 200) {
        return MLModelsStatusResponseModel.fromJson(response.data);
      } else {
        throw ServerException(
          message: 'Error al obtener estado de modelos: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } on DioException catch (e) {
      throw HttpErrorHandler.handle(e);
    } catch (e) {
      if (e is AppException) {
        rethrow;
      }
      throw ServerException(
        message: 'Error inesperado al obtener estado de modelos: $e',
      );
    }
  }
}
